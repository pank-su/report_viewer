<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/material-theme/theme.css"/>
    <link rel="stylesheet" type="text/css" href="/static/styles/general.css"/>

    <title>Test</title>
</head>
<script>
    function toggleVisibility(id) {
        let e = document.getElementById(id);
        e.style.display = ((e.style.display !== 'none') ? 'none' : 'block');
    }
</script>
<body>
<div class="myAppBar surface-secondary">
    <button class="icon-button" onclick="toggleVisibility('rail')">
        <img src="/static/images/leading-icon.png"/>
    </button>

    <p class="title-large title">
        ReportViewer
    </p>
</div>
<div id="rail" class="navigation-rail surface-first">
    <button class="fab tertiary-container ">
        <img src="../static/images/edit.png">
    </button>
    <nav class="navs">
        <a class="nav active">
            <div class="naaav">
                <img class="icon" src="/static/images/design_services.png"/>
                <p class="label-medium" style="text-align: center">
                    Editor
                </p>
            </div>

        </a>
        <a class="nav">
            <div class="naaav" href="/about">
                <img class="icon" src="/static/images/help.png"/>
                <p class="label-medium" style="text-align: center">
                    About
                </p>
            </div>
        </a>
        <a class="nav active" href="/contact">
            <div class="naaav">
                <img class="icon" src="/static/images/contacts.png"/>
                <p class="label-medium" style="text-align: center">
                    Contact
                </p>
            </div>

        </a>

    </nav>
</div>


</body>
</html>