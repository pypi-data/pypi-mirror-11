{%- extends 'full.tpl' -%}

{% block output_group -%}

<div class="output_hidden">
{{ super() }}
</div>

{% endblock output_group %}

{%- block header -%}

{{ super() }}

<style type="text/css">

div.input_wrapper {
    margin-top: 0px;
}

.output_hidden {
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

<!-- <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script> -->
<script>
// $(document).ready(function(){
//   $(".input_wrapper").click(function(){
//       $(this).prev('.output_hidden').slideToggle();
//   });
// })
</script>

{%- endblock header -%}