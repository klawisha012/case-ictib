
// // Добавляем обработку клика и перетаскивания файлов
// document.addEventListener('DOMContentLoaded', function () {
//     const dropZone = document.getElementById('upload_container');
//     const fileInput = document.getElementById('videoUpload');

//     // Обработчик перетаскивания
//     dropZone.addEventListener('dragover', function (e) {
//         e.preventDefault();
//         e.stopPropagation();
//         dropZone.classList.add('dragover');
//     });

//     dropZone.addEventListener('dragleave', function (e) {
//         e.preventDefault();
//         e.stopPropagation();
//         dropZone.classList.remove('dragover');
//     });

//     dropZone.addEventListener('drop', function (e) {
//         e.preventDefault();
//         e.stopPropagation();
//         dropZone.classList.remove('dragover');

//         const files = e.dataTransfer.files;
//         if (files.length > 0) {
//             handleFileUpload(files[0]);
//         }
//     });

//     fileInput.addEventListener('change', function () {
//         if (fileInput.files.length > 0) {
//             handleFileUpload(fileInput.files[0]);
//         }
//     });

//     function handleFileUpload(file) {
//         const formData = new FormData();
//         formData.append("file", file); //{"file": *файл*}
//         fetch("/", {
//             method: "POST",
//             body: formData,
//         })
//         .then(response => response.json())
//         .then((data)=>{
//             if(data.success) {
//                 document.getElementById("result").innerHTML = `<a href="${data.file_url}" download>Скачать обработанное видео</a>`;
//             }
//             else{
//                 document.getElementById("error-message").textContent = data.error;
//             }
//         })
//         .catch((err) => {
//             document.getElementById("error-message").textContent  = "Ошибка загрузки: " + err.message;
//         });
//     }
// });



// document.getElementById("upload_container").addEventListener("submit", async function (event) {
//     event.preventDefault(); // Отменяем стандартное поведение формы

//     const fileInput = document.getElementById("videoUpload");
//     const file = fileInput.files[0];

//     //const formData = new FormData();

//     if (!file) {
//         alert("Пожалуйста, выберите видео для загрузки.");
//         return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);

//     try {
//         const response = await fetch("/upload", { //
//             method: "POST",
//             body: formData,
//         });

//         if (response.ok) {
//             // Получаем ссылку на обработанное видео от сервера
//             const data = await response.json();
//             const processedVideoUrl = data.processed_video_url;

//             // Делаем видимым блок с кнопкой загрузки
//             const downloadContainer = document.getElementById("download_container");
//             downloadContainer.style.display = "block";

//             // Устанавливаем ссылку для кнопки загрузки
//             const downloadButton = document.getElementById("download_button");
//             downloadButton.onclick = function () {
//                 window.location.href = processedVideoUrl; // Скачивание обработанного видео
//             };
//         } else {
//             document.getElementById("error-message").textContent = "Ошибюка: " + response.error.message
//         }
//     } catch (err) {
//         console.error("Ошибка:", error);
//         alert("Произошла ошибка при загрузке видео.");
//     }
// });

document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('upload_container');
    const fileInput = document.getElementById('videoUpload');
    const errorMessage = document.getElementById('error-message');
    const result = document.getElementById('result');
    const downloadContainer = document.getElementById('download_container');
    const downloadButton = document.getElementById('download_button');

    // Общий обработчик файлов
    async function handleFileUpload(file) {
        // Очистка сообщений
        errorMessage.textContent = "";
        result.innerHTML = "";

        // Проверка формата файла
        const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv'];
        if (!allowedTypes.includes(file.type)) {
            errorMessage.textContent = "Недопустимый формат файла. Разрешены только: MP4, AVI, MOV, MKV.";
            return;
        }

        // Проверка размера файла (например, максимум 2 ГБ)
        const maxSize = 2 * 1024 * 1024 * 1024;
        if (file.size > maxSize) {
            errorMessage.textContent = "Файл слишком большой. Максимальный размер: 2 Гб МБ.";
            return;
        }

        // Подготовка и отправка запроса
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                const processedVideoUrl = data.file_url;

                result.innerHTML = `<a href="${processedVideoUrl}" download>Скачать обработанное видео</a>`;
                downloadContainer.style.display = "block";

                downloadButton.onclick = function () {
                    window.location.href = processedVideoUrl;
                };
            } else {
                const errorData = await response.json();
                errorMessage.textContent = errorData.error || "Произошла ошибка на сервере.";
            }
        } catch (err) {
            console.error("Ошибка загрузки:", err);
            errorMessage.textContent = "Не удалось загрузить видео. Проверьте соединение.";
        }
    }

    // Обработчик перетаскивания
    dropZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    // Обработчик выбора файла через input
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            handleFileUpload(fileInput.files[0]);
        }
    });

    // Обработчик отправки формы
    dropZone.addEventListener("submit", function (e) {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) {
            errorMessage.textContent = "Пожалуйста, выберите видео для загрузки.";
            return;
        }
        handleFileUpload(file);
    });
});
