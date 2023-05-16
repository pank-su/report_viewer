% rebase('layout.tpl', title=title, userExist=userExist)

<div class="grid">
    % for order in orders:
    <div class="card">
        <div class="in-card">
            <img class="round-avatar"
                 src="{{order['user_image']}}"/>
            <div style="gap: 4px" class="column fill-width-card">
                <p>{{order['name']}}</p>
                <div class="row space-bt">
                    <p>{{order['description']}}</p>
                    <p>{{order['price']}} ₽</p>
                </div>
            </div>
        </div>
        <img class="end-card"
             src="{{order['image_path']}}"/>
    </div>
    % end
</div>
<form action="/submit_order" method="post" enctype="multipart/form-data">
  <label for="order_name">Название заказа:</label>
  <input type="text" id="order_name" name="order_name" required>

  <label for="order_description">Описание заказа:</label>
  <textarea id="order_description" name="order_description" required></textarea>

  <label for="order_price">Цена:</label>
  <input type="number" id="order_price" name="order_price" required>

  <label for="order_due_date">Дата исполнения:</label>
  <input type="date" id="order_due_date" name="order_due_date" required>

  <label for="order_phone">Телефон обратной связи:</label>
  <input type="tel" id="order_phone" name="order_phone" placeholder="Введите ваш телефонный номер" required>

  <label for="order_image">Выберите картинку:</label>
  <input type="file" id="order_image" name="order_image" accept="image/*" required>


  <input type="submit" value="Отправить заказ">
</form>