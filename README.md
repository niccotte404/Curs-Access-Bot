# Curs-Access-Bot
## Бот для проверки доступа к платному курсу
Это своего рода security bot, который предотвращает попадание нежелательных лиц на курс<br>
Он работает в качестве замены администратора, проверяющего наличие оплаты и выдающего доступ к курсу<br>
<br>
### Реализация: <br>
- Принимает сообщение пользователя<br>
- Должен был проверять отправелнное на почту письмо об оплате (от платежной системы).<br>
Но, увы, сколько ни копался с этим, так и не смог найти, как это сделать.<br>
Поэтому сейчас планирую дописать генерацию пароля и его проверку (тут все зависит от сайта, с которого приходит письмо с доступом на курс,<br>
т.к именно в бэкэнде сайта нужно писать генерацию пароля, а проверку уже в самам боте)
- Ну и присалает письмо администратору на почту о том, что пользователь прошел проверку (так, на всяий случай)
- Можно сделать еще генерацию ссылки на курс (но тут опять же все зависит от платформы)
<br>
Вообще, мне нравится эта задумка. Бот просто убирает лишние траты на всяких администраторов.<br>
Но его написание имеет зависимость от других платформ курса.
