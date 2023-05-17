% rebase('layout.tpl', title=title, userExist=userExist)

<div class="grid">
    % for order in orders:
    <div class="card">
        <div class="in-card">
            <img class="round-avatar"
                 src="{{order['user_image']}}"/>
            <div style="gap: 4px" class="column fill-width-card">
                <p>{{order['name']}}</p>
                <p>{{order['description']}}</p>
                <div class="row space-bt">
                    <p>TODO {{order['date_complete']}}</p>
                    <p>{{order['price']}} ₽</p>
                </div>
            </div>
        </div>
        <img class="end-card"
             src="{{order['image_path']}}"/>
    </div>
    % end
</div>
% if userExist:
<form action="/submit_order" method="post" enctype="multipart/form-data">
  <label for="order_name">Order name:</label>
  <input type="text" id="order_name" name="order_name" required>

  <label for="order_description">Order description:</label>
  <textarea id="order_description" name="order_description" required></textarea>

  <label for="order_price">Price:</label>
  <input type="number" id="order_price" name="order_price" required>

  <label for="order_due_date">Date complete:</label>
  <input type="date" id="order_due_date" name="order_due_date" required>

  <label for="order_phone">Phone for feedback:</label>
  <input type="tel" id="order_phone" name="order_phone" placeholder="+7 999 999999" required>

  <label for="order_image">Choose image:</label>
  <input type="file" id="order_image" name="order_image" accept="image/*" required>

  <input type="submit" value="Send order">
</form>
% end
% if not userExist:
        <div style="width: 100%; margin: auto;max-width: 500px; text-align: center;">
            <p style="text-align: center;">For using adding new orders you need authorised</p>
            <a style="display: inline-block; margin-top: 10px;" href="https://gnfhxumqcggerkhmzajj.supabase.co/auth/v1/authorize?provider=github">
                <button class="primary filledButton">
                    Sign In with GitHub
                </button>
            </a>

        </div>
 % end
<script>
    % if len(error) > 0:
    alert("{{error}}")
    % end
</script>