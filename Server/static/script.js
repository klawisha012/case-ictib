document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById("upload_container");
    const fileInput = document.getElementById("videoUpload");
    const errorMessage = document.getElementById("error-message");
    const resultContainer = document.getElementById("download_container");

    // Обработчик отправки формы
    dropZone.addEventListener("submit", function (event) {
        event.preventDefault(); // Останавливаем стандартное поведение формы

        const file = fileInput.files[0];
        if (!file) {
            errorMessage.textContent = "Выберите файл для загрузки.";
            return;
        }

        handleFileUpload(file);
    });

    function getCSRFToken() {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        return csrfToken;
    }

    // Обработчики для drag-and-drop
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

    function handleFileUpload(file) {
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            document.getElementById("error-message").textContent = "Не удалось получить CSRF-токен.";
            return;
        }

        errorMessage.textContent = "";
        resultContainer.innerHTML = "";

        const formData = new FormData();
        formData.append("file", file);

        fetch("/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        })

        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                resultContainer.innerHTML = `<a href="${data.file_url}" download>Скачать обработанное видео</a>`;
            } else {
                errorMessage.textContent = data.error || "Произошла ошибка при обработке.";
            }
        })
        .catch(err => {
            errorMessage.textContent = "Ошибка загрузки: " + err.message;
        });
    }
});
