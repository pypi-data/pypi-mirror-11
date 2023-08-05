{%- extends 'full.tpl' -%}

{% block input_group -%}

<div class="input_hidden">
{{ super() }}
</div>

{% endblock input_group %}

{%- block header -%}

{{ super() }}

<style type="text/css">

div.output_wrapper {
    margin-top: 0px;
}

.input_hidden {
  display: none;
  margin-top: 5px;
}

div.prompt {
    display: none;
}

div.cell{
    max-width:90%;
    margin-left:auto;
    margin-right:auto;
}

div.text_cell_render{
    max-width:90%;
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

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script>
$(document).ready(function(){
  $(".output_wrapper").click(function(){
      $(this).prev('.input_hidden').slideToggle();
  });
})
</script>

{%- endblock header -%}