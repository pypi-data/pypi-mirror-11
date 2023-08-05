{%- extends 'full.tpl' -%}

{% block output_group -%}
{% endblock output_group %}

{%- block header -%}

{{ super() }}

<style type="text/css">

div.input_wrapper {
    margin-top: 0px;
}

div.prompt {
    /*display: none;*/
}

div.cell{
    /*max-width:90%;*/
    margin-left:auto;
    margin-right:auto;
}

div.text_cell_render{
    /*max-width:90%;*/
    margin-left:auto;
    margin-right:auto;
}

pre, code, kbd, samp {
     font-family: Consolas, monospace;
     font-size: 12px;
}

p {
    font-size:14px;
}

h1 {
    /*text-align: center;*/
}

.CodeMirror{
    /*font-family: "Consolas", sans-serif;*/
}

</style>

{%- endblock header -%}
