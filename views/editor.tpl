% rebase('layout.tpl', title='Editor', userExist=userExist)

<script src="https://cdn.jsdelivr.net/gh/xxjapp/xdialog@3/xdialog.min.js"></script>
<div class="twos" id="editor_page" style="display: grid; width: 100%">
    % if userExist:
    <div id="files" class="surface-first">
        <button class="primary filledButton fileButton" onclick="fileSend()">Add file</button>
        % for file in files:
        <button class="fileButton surface-first" onclick="selectThis(this)">{{file["name"]}}</button>
        % end
    </div>
    % end
    <div id="editor" class="surface-first">
        % if userExist:
        <textarea readonly id="enterArea" onchange="onEdit(this.value)" class="area" aria-label="">You can edit in this space</textarea>
        % end
        % if not userExist:
        <div>
            <p>For using this app you need authorised</p>
            <a href="https://gnfhxumqcggerkhmzajj.supabase.co/auth/v1/authorize?provider=github">
                <button class="primary filledButton">
                    Sign In with GitHub
                </button>
            </a>

        </div>
        % end
    </div>
    <iframe id="preview" src="/preview">
    </iframe>
    <button id="shareButton" onclick="copyText(document.location.href + '/s/{{user_id}}/' + selectedFile)"
            class="primary-container">
        <img src="/static/images/share.png"/>
    </button>
</div>
<script>


    var selectedFile = ""

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
                document.getElementById('preview').contentWindow.location.reload();
            }
        };
        var data = JSON.stringify({"data": text, "filename": selectedFile});
        xhr.send(data);
    }

    function copyText(text) {
        navigator.clipboard.writeText(text);
        openDialog("Ссылка скопирована в буфер обмена")
    }


    function addClass() {
        document.getElementById("editor_page").classList.add("threes")
    }

    function selectThis(btn) {
        btn.classList.add('selected')
        fileButtons = document.getElementsByClassName('fileButton')
        for (let fileButton of fileButtons) {
            if (fileButton === btn) {

            } else if (fileButton.classList.contains('selected')) {
                fileButton.classList.remove('selected')
            }
        }
        selectedFile = btn.textContent
        xhr.open("GET", "/content/" + btn.textContent, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                document.getElementById("enterArea").removeAttribute("readonly")
                document.getElementById("enterArea").textContent = xhr.responseText

            } else if (xhr.readyState === 4 && xhr.status === 400) {
                document.getElementById("enterArea").setAttribute("readonly", "")
                document.getElementById("enterArea").textContent = xhr.responseText
            }
        };
        xhr.send()
        document.getElementById("preview").src = "/preview/" + selectedFile
    }

    function fileSend() {
        const input = document.createElement('input');
        input.type = 'file';

        input.onchange = e => {
            let file = e.target.files[0];
            const form = new FormData()
            form.append("file", file)
            fetch("/upload", {method: "POST", body: form}).then(function (r) {
                // если файл загрузился, то перезагружаем страницу
                if (r.ok) {
                    location.reload()
                }
            })
        }
        input.click();
    }

    function openDialog(text){
        xdialog.open({
                title: null,
                body: text,
                style: 'text-align:center;',
                buttons: ['ok']
            })
    }

    // Если пользователь есть, то добавляем класс к основному div, для изменения стилей
    % if userExist:
    addClass()
    % end


</script>