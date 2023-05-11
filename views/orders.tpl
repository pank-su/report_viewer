% rebase('layout.tpl', title=title, userExist=userExist)

<div class="grid">
    % for order in orders:
    <div class="card">
        <div class="in-card">
            <img class="round-avatar"
                 src="https://sun9-40.userapi.com/impg/BFGPnEaCrirYv9QS9PXF-1HL0IlkvmE-5xAbVw/5574gl963Ag.jpg?size=1627x2160&quality=95&sign=d1053c00be7df8f1540c97823683131f&type=album"/>
            <div style="gap: 4px" class="column fill-width-card">
                <p>Название товара</p>
                <div class="row space-bt">
                    <p>Описание</p>
                    <p>Цена</p>
                </div>
            </div>
        </div>
        <img class="end-card"
             src="https://sun9-40.userapi.com/impg/BFGPnEaCrirYv9QS9PXF-1HL0IlkvmE-5xAbVw/5574gl963Ag.jpg?size=1627x2160&quality=95&sign=d1053c00be7df8f1540c97823683131f&type=album"/>
    </div>
    % end
</div>