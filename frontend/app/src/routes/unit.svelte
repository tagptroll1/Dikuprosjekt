<body>
<div id="editor"> def test():
    return "Success!"
</div>
  <div>
    <style type="text/css" media="screen">
          #editor {
              position: absolute;
              top: 0;
              right: 0;
              bottom: 0;
              left: 0;
          }
      </style>
    <script src="https://pagecdn.io/lib/ace/1.4.6/ace.js" type="text/javascript" charset="utf-8"></script>
    
    <script>
          //console.log(ace)
          var editor = ace.edit("editor");
          editor.setTheme("ace/theme/monokai");
          editor.session.setMode("ace/mode/python");
    </script>
  </div>
</body>
