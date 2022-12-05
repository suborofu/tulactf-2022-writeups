<?php 

require __DIR__ . '/vendor/autoload.php'; 
require 'utils/functions.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

define('COOKIE_KEY', 'user');
define('JWT_SECRET', 'butterfly');
define('IMAGE_FORM_NAME', 'the_best_image_of_TulaCTF_2022');
$path = __DIR__ . '/uploads/';

$isAdmin = false;
$isAuth = false;

// Разрешенные расширения файлов.
$allow = array();
 
// Запрещенные расширения файлов.
$deny = array(
	'phtml', 'php', 'php3', 'php4', 'php5', 'php6', 'php7', 'phps', 'cgi', 'pl', 'asp', 
	'aspx', 'shtml', 'shtm', 'htaccess', 'htpasswd', 'ini', 'log', 'sh', 'js', 'html', 
	'htm', 'css', 'sql', 'spl', 'scgi', 'fcgi'
);

if(isset($_COOKIE[COOKIE_KEY])){
    try{
        $decoded = JWT::decode($_COOKIE[COOKIE_KEY], new Key(JWT_SECRET, 'HS256'));
        $isAdmin = $decoded->role == 'admin';
        $isAuth = true;
    } catch(Exception $e){
        if($e->getMessage() == 'Signature verification failed'){
            setcookie(COOKIE_KEY, null, -1);
        }
    }
} else {
    if(isset($_POST['doLogin'])){
        $payload = [
            'role' => 'guest',
        ];
        $jwt = JWT::encode($payload, JWT_SECRET, 'HS256');
        setcookie(COOKIE_KEY, $jwt);
    }
}
if($isAdmin && !empty($_FILES[IMAGE_FORM_NAME])){
    $file = $_FILES[IMAGE_FORM_NAME];
    $parts = pathinfo($file['name']);
    if($file['error'] == 0){
        $error = '';
        if (empty($file['name']) || empty($parts['extension'])) {
            $error = 'Недопустимое тип файла';
        } elseif (!empty($allow) && !in_array(strtolower($parts['extension']), $allow)) {
            $error = 'Недопустимый тип файла';
        } elseif (!empty($deny) && in_array(strtolower($parts['extension']), $deny)) {
            $error = 'Недопустимый тип файла';
        } 
        if($error) {
            die($error);
        }
        system('convert -size 1024x800 ' . $file['tmp_name'] . ' ' . $path . md5($file['name']) . '.png');
        echo json_encode(['file' => '/uploads/' . md5($file['name']) . '.png']);
    } else {
        $error = 'Не удалось загрузить файл.';
    }
    die();
}



?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TulaCTF 2022</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous">
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.1/jquery.min.js"
        integrity="sha512-aVKKRRi/Q/YV+4mjoKBsE4x3H+BkegoM/em46NNlCqNTmUYADjBbeNefNxYV7giUp0VxICtqdrbqU7iVaeZNXA=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <script src="/public/js/ajaxupload.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css">
</head>
<style>
.form-wrap {
    height: 100vh;
}
body{
    background: #f5f5f5;
}
</style>

<body>
    <div class="container">
        <header class="d-flex flex-wrap justify-content-md-center justify-content-between py-3 mb-4 border-bottom">
            <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">

                <span class="fs-4">Прослушано в Гостинке</span>
            </a>

            <ul class="nav nav-pills">
                <li class="nav-item"><a href="#" class="nav-link active" aria-current="page">Главная</a></li>
                <?php if($isAdmin){ ?>
                <li class="nav-item"><a href="#" class="nav-link" aria-current="page" data-bs-toggle="modal"
                        data-bs-target="#postModal">Написать пост</a>
                </li>
                <?php } ?>
                <?php if($isAuth){ ?>
                <li class="nav-item"><a href="#" class="nav-link" aria-current="page" onclick="dropSession()">Выйти</a>
                </li>
                <?php } else { ?>
                <li class="nav-item"><a href="#" class="nav-link" aria-current="page" data-bs-toggle="modal"
                        data-bs-target="#exampleModal">Войти</a></li>
                <?php }?>
            </ul>
        </header>
        <div class="row" style="max-width: 600px; margin: 0 auto;">
            <div class="col-12 my-2">
                <div class="card">
                    <img src="/public/img/dora.jpg"" class="card-img-top" alt="...">
                    <div class="card-body">
                        <p class="card-text">Люблю Дору<br>Анон</p>
                        
                        <div class="text-muted">2 часа назад</div>
                        <?php if($isAuth){ ?>
                        <a href="#" class="btn btn-light like-btn"><i class="bi bi-heart"></i></a>
                        <?php } ?>
                    </div>
                </div>
            </div>
            <div class="col-12 my-2">
                <div class="card">
                    <div class="card-body">
                        <p class="card-text">понравился мальчик, ехали на 35 лайне в мясново 1 декабря в 17:45, сидели рядом в конце салона, я вышла у медсанчасти №5, а ты поехал дальше<br>
Найтись пожалуйста 🙏<br>
Анон<br>
Адмиру печенек с корицей 🍪💗</p>
                        <div class="text-muted">14 часов назад</div>
                        <?php if($isAuth){ ?>
                        <a href="#" class="btn btn-light like-btn"><i class="bi bi-heart"></i></a>
                        <?php } ?>
                    </div>
                </div>
            </div>
            
            <div class="col-12 my-2">
                <div class="card">
                <iframe height="300" src="https://www.youtube.com/embed/jumQ76GEYLQ?start=10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <iframe height="300" src="https://www.youtube.com/embed/JsD5jUralB8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    <div class="card-body">
                        <p class="card-text">Помогите выбрать мелодию для будильника пж<br>
                        Админу печенек<br>
                        Анон</p>
                        <div class="text-muted">вчера в 04:21</div>
                        <?php if($isAuth){ ?>
                        <a href="#" class="btn btn-light like-btn"><i class="bi bi-heart"></i></a>
                        <?php } ?>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <?php if(!$isAuth){ ?>
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Авторизация</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form method="post">
                        <div class="mb-3">
                            <label for="exampleInputLogin1" class="form-label">Ваш логин</label>
                            <input type="login" class="form-control" id="exampleInputLogin1"
                                aria-describedby="loginHelp">
                            <div id="loginHelp" class="form-text">Придумайте уникальный логин, это важно.</div>
                        </div>
                        <div class="mb-3">
                            <label for="exampleInputPassword1" class="form-label">Пароль</label>
                            <input type="password" class="form-control" id="exampleInputPassword1"
                                aria-describedby="passwordHelp">
                            <div id="passwordHelp" class="form-text">Пароль должен содержать 4 уникальных спецсимвола,
                                символ "тильда" и 2 цифры.</div>
                        </div>
                        <button type="submit" class="btn btn-primary" name="doLogin">Войти</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <?php } ?>
    <?php if($isAdmin){ ?>
    <div class="modal fade" id="postModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Создание поста</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form method="post" enctype="multipart/form-data">
                        <label for="exampleInputimage1" class="form-label">Изображение поста</label>
                        <input type='file' name="<?= IMAGE_FORM_NAME; ?>" class="form-control" id="imagePost"
                            aria-describedby="imageHelp">
                        <div>
                        <label for="exampleInputimage1" class="form-label">Текст</label>
                        <textarea class="form-control" name="text" id="" cols="30" rows="10" id="exampleInputimage2"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary" name="setImage">Отправить</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <script>
        const imagePostBtn = $('#imagePost')
        new AjaxUpload(imagePostBtn, {
                action: '/',
                name: '<?= IMAGE_FORM_NAME; ?>',
                onSubmit: function(file, ext){
                    if (! (ext && /^(jpg|png|jpeg|gif|svg)$/i.test(ext))){
                        alert('Ошибка! Разрешены только картинки');
                        return false;
                    }

                },
                onComplete: function(file, response){
                    response = JSON.parse(response);
                    $('#imagePost').after(`<img src="${response.file}" alt="" style="width: 100%; height: auto;">`)
                }
            });
    </script>
    <?php } ?>
    <script>
    function dropSession() {
        console.log('safr')
        document.cookie = `<?= COOKIE_KEY; ?> =; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        location.reload();
    }
    $('.like-btn').click(function() {
        if ($(this).find('i').hasClass('bi-heart-fill')) {
            $(this).find('i').removeClass('bi-heart-fill');
            $(this).find('i').addClass('bi-heart');
        } else {
            $(this).find('i').removeClass('bi-heart');
            $(this).find('i').addClass('bi-heart-fill');
        }
    });
    </script>
</body>

</html>