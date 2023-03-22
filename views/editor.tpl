% rebase('layout.tpl', title='Editor')

<div style="display: grid; grid-template-columns: 1fr 1fr; width: 100%">
    <div id="editor" class="surface-first">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label class="label-large">Отправьте ваш крутой файл к нам</label>
            <input type="file"
                   id="inputFile" name="inputFile"

                   accept=".docx, .org, .md, .txt, .html, .tex">
            <input type="submit" id="submit">
        </form>
    </div>
    <iframe id="preview" src="../preview/test.html">
    </iframe>

</div>