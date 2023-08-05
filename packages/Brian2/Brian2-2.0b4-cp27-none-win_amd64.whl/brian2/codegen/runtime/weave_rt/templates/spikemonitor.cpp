{% import 'common_macros.cpp' as common with context %}
{% macro main() %}
    {{ common.insert_pointers_lines() }}

    {# USES_VARIABLES { t, i, _clock_t, count,
                        _source_start, _source_stop} #}
    {#  Get the name of the array that stores these events (e.g. the spikespace array) #}
    {% set _eventspace = get_array_name(eventspace_variable) %}

	int _num_events = {{_eventspace}}[_num{{eventspace_variable.name}}-1];
    if (_num_events > 0)
    {
        // For subgroups, we do not want to record all spikes
        // We assume that spikes are ordered
        int _start_idx = _num_events;
        int _end_idx = _num_events;
        for(int _j=0; _j<_num_events; _j++)
        {
            const int _idx = {{_eventspace}}[_j];
            if (_idx >= _source_start) {
                _start_idx = _j;
                break;
            }
        }
        for(int _j=_start_idx; _j<_num_events; _j++)
        {
            const int _idx = {{_eventspace}}[_j];
            if (_idx >= _source_stop) {
                _end_idx = _j;
                break;
            }
        }
        _num_events = _end_idx - _start_idx;
        if (_num_events > 0) {
            const int _vectorisation_idx = 1;
            {{scalar_code|autoindent}}
            // Get the current length and new length of t and i arrays
            const int _curlen = {{_dynamic_t}}.attr("shape")[0];
            const int _newlen = _curlen + _num_events;
            // Resize the arrays
            py::tuple _newlen_tuple(1);
            _newlen_tuple[0] = _newlen;
            _owner.mcall("resize", _newlen_tuple);
            // Get the potentially newly created underlying data arrays
            double *_t_data = (double*)(((PyArrayObject*)(PyObject*){{_dynamic_t}}.attr("data"))->data);
            // TODO: How to get the correct datatype automatically here?
            npy_int32 *_i_data = (npy_int32*)(((PyArrayObject*)(PyObject*){{_dynamic_i}}.attr("data"))->data);
            {% for varname, var in record_variables.items() %}
            {{c_data_type(var.dtype)}}* _{{varname}}_data = ({{c_data_type(var.dtype)}}*)(((PyArrayObject*)(PyObject*){{get_array_name(var, access_data=False)}}.attr("data"))->data);
            {% endfor %}
            // Copy the values across
            for(int _j=_start_idx; _j<_end_idx; _j++)
            {
                const int _idx = {{_eventspace}}[_j];
                const int _vectorisation_idx = _idx;
                {{vector_code|autoindent}}
                _t_data[_curlen + _j - _start_idx] = _clock_t;
                _i_data[_curlen + _j - _start_idx] = _idx - _source_start;
                {% for varname in record_variables | sort%}
                _{{varname}}_data[_curlen + _j - _start_idx] = _to_record_{{varname}};
                {% endfor %}
                {{count}}[_idx - _source_start]++;
            }
        }
	}
{% endmacro %}

{% macro support_code() %}
{% endmacro %}
