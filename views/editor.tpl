% rebase('layout.tpl', title='Editor')

<div style="display: grid; grid-template-columns: 1fr 1fr; width: 100%">
    <div id="editor" class="surface-first">
        % if filecontent == "":
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label class="label-large">Отправьте ваш крутой файл к нам</label>
            <input type="file"
                   id="inputFile" name="inputFile"

                   accept=".docx, .org, .md, .txt, .html, .tex">
            <input type="submit" id="submit">
        </form>
        % end
        % if filecontent != "":
        <textarea class="area" onchange="onEdit(this.value)">
                {{filecontent}}
            </textarea>
        % end
    </div>
    <iframe id="preview" src="/preview">
    </iframe>
    <button id="shareButton" onclick="copyText(window.location.hostname + '/preview/{{secret}}')" class="primary-container">
        <img src="../static/images/share.png"/>
    </button>
</div>
<script>


    function onEdit(text) {
        let xhr = new XMLHttpRequest();
        let url = "/preview_reload";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var json = JSON.parse(xhr.responseText);
                console.log(json.email + ", " + json.password);
            }
        };
        var data = JSON.stringify({"data": text});
        xhr.send(data);
        setTimeout(function() {
            document.getElementById('preview').contentWindow.location.reload();
        }, 500);
    }

    function copyText(text) {
        navigator.clipboard.writeText(text);
    }

</script>