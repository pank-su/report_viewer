% rebase('layout.tpl', title='Editor')

<div style="display: grid; grid-template-columns: 1fr 1fr; width: 100%">
    <div id="editor" class="surface-first">
        % if userExist:
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label class="label-large">Отправьте ваш крутой файл к нам</label>
            <input type="file"
                   id="inputFile" name="inputFile"

                   accept=".docx, .org, .md, .txt, .html, .tex">
            <input type="submit" id="submit">
        </form>
        % end
        % if not userExist:
        <div>
            <p>For using this app you need authorised</p>
            <a href="https://gnfhxumqcggerkhmzajj.supabase.co/auth/v1/authorize?provider=github">
                <button class="GitHub">
                    <p>Войти с помощью GitHub</p>
                </button>
            </a>

        </div>
        % end
    </div>
    <iframe id="preview" src="/preview">
    </iframe>
    <button id="shareButton" onclick="copyText(document.location.hostname + '/preview/null')"
            class="primary-container">
        <img src="../static/images/share.png"/>
    </button>
</div>
<script>

    // Исправляем ссылку с oauth 2 на нужную для чтения bottle
    if (document.location.href.includes("/#"))
        document.location = document.location.href.replace("/#", "/?")

    var xhr = new XMLHttpRequest();

    function onEdit(text) {

        let url = "/preview_reload";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var json = JSON.parse(xhr.responseText);
                // console.log(json.email + ", " + json.password);
            }
        };
        var data = JSON.stringify({"data": text});
        xhr.send(data);
        setTimeout(function () {
            document.getElementById('preview').contentWindow.location.reload();
        }, 500);
    }

    function copyText(text) {
        navigator.clipboard.writeText(text);
        alert("Ссылка скопирована в буфер обмена")
    }

</script>