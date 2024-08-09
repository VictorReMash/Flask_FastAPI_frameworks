Запуск программы, через аргументы командной строки с указанием метода:
--method threads;
--method processes;
--method async;
--method sync (можно не указывать, отработает по умолчанию)
Пример:
python main.py https://example.com/image1.jpg https://example.com/image2.png --method async
