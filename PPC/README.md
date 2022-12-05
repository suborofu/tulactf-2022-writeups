# Multipass

Исходник:

- [MEGA](https://mega.nz/file/2fgXABpI#nEITBDgLJquTlHFVgwtXtxLY8t2cTFCAj9Cn2EXdxmM)
- [GOOGLE](https://drive.google.com/file/d/1uY5vryJLqaUYY1czCfK-X7WU6f6r5YxO/view?usp=share_link)

**10000** паспортов в **Base64**, на одном из них в разделе ФИО стоит флаг, начинающийся на **TulaCTF**. Можно с помощью OCR обработать все фото и вытянуть текст, при совпадении рассмотреть фото подробнее. Если использовать [OpenModelZoo](https://github.com/openvinotoolkit/open_model_zoo/tree/master/demos/text_spotting_demo/python), ответ можно найти за 1.5-2 часа.

# Flashka ot Deda

Исходник:

- [GOOGLE](https://drive.google.com/file/d/1FPDyx1vdzzyc8JsOKuH8ewaZoZyZrGOw/view?usp=share_link)
- [MEGA](https://mega.nz/file/qeRgSLzC#ecvmLr3bE0IZ9oR34rAHTQM8k8JsC9pO8GMYVT6YkfA)

На видео изображен процесс работы с перфокартами. Само видео имеет формат **MOV**, который может иметь альфа-канал. Разбив видео на кадры (3387 png'ешек), посмотрим на содержимое альфа-канала. В нем встречаются прямоугольники размером **8x20** пикселей, т.е. кадр состоит из 80 прямоугольников в ширину и 12 прямоугольников в высоту. Это напоминает структуру перфокарты. Вот... Таким образом, в каждом кадре зашифровано сообщение с помощью кодировки методом перфокарты. Дальше надо раскодировать и получить файл.
