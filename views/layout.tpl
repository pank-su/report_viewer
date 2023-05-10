<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/material-theme/theme.css"/>
    <link rel="stylesheet" type="text/css" href="/static/styles/general.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/xxjapp/xdialog@3/xdialog.min.css">

    <title>Report Viewer - {{title}}</title>
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
    % if userExist:
    <a class="icon-button" href="/logout">
        <img style="width: 24px; height: 24px" src="/static/images/logout.png"/>
    </a>
    % end
</div>
<div style="display: flex; flex-direction: row; height: 93%;">
    <div id="rail" class="navigation-rail surface-first">
        <a class="fab tertiary-container " href="/editor">
            <img src="/static/images/edit.png">
        </a>
        <nav class="navs">
            <a class="nav" id="nav1" href="/editor">
                <div class="naaav">
                    <img class="icon" src="/static/images/design_services.png"/>
                    <p class="label-medium" style="text-align: center">
                        Editor
                    </p>
                </div>
            </a>
            <a class="nav" id="nav2" href="/about">
                <div class="naaav">
                    <img class="icon" src="/static/images/help.png"/>
                    <p class="label-medium" style="text-align: center">
                        About
                    </p>
                </div>
            </a>
            <a class="nav" id="nav3" href="/contact">
                <div class="naaav">
                    <img class="icon" src="/static/images/contacts.png"/>
                    <p class="label-medium" style="text-align: center">
                        Contact
                    </p>
                </div>
            </a>
            <a class="nav" id="nav4" href="/orders">
                <div class="naaav">
                    <img class="icon" src="/static/images/order.png"/>
                    <p class="label-medium" style="text-align: center">
                        Orders
                    </p>
                </div>
            </a>
        </nav>
    </div>
    <div class="content surface-first">
        {{!base}}
    </div>
</div>


</body>
<script>

    function checkTitle(titleName) {
        switch (titleName) {
            case 'Editor':
                document.getElementById("nav1").classList.add("active")
                break;
            case 'Contact':
                document.getElementById("nav3").classList.add("active")
                break;
            case 'About us':
                document.getElementById("nav2").classList.add("active")
                break;

        }
    }

    checkTitle("{{title}}")
</script>
</html>