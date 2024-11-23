document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById("upload_container");
    const fileInput = document.getElementById("videoUpload");
    const errorMessage = document.getElementById("error-message");
    const resultContainer = document.getElementById("download_container");
    const downloadButton = document.getElementById("download_button");
    const fileNameDisplay = document.getElementById("file-name-display");
    const uploadContainer = document.getElementById("upload_container");

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = `Выбран файл: ${fileInput.files[0].name}`;
        } else {
            fileNameDisplay.textContent = "Файл не выбран";
        }
    });
    
    uploadContainer.addEventListener("drop", function (e) {
        e.preventDefault();
        e.stopPropagation();

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files; // Устанавливаем файл в input
            fileNameDisplay.textContent = `Выбран файл: ${files[0].name}`;
        }
    });

    uploadContainer.addEventListener("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
    });

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
    dropZone.addEventListener("submit", function (event) {
        event.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            errorMessage.textContent = "Пожалуйста, выберите файл.";
            errorMessage.style.display = "block";
            return;
        }

        handleFileUpload(file);
    });

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
            fileInput.files = files; // Устанавливаем файл в input
        }
    });

    function handleFileUpload(file) {
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            document.getElementById("error-message").textContent = "Не удалось получить CSRF-токен.";
            return;
        }

        //errorMessage.textContent = "";
        //resultContainer.innerHTML = "";

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
                resultContainer.style.display = "block";
                downloadButton.onclick = function () {
                    const a = document.createElement("a");
                    a.href = data.file_url;
                    a.download = data.file_name;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                };
            } else {
                errorMessage.textContent = data.error || "Произошла ошибка при обработке.";
            }
        })
        .catch(err => {
            errorMessage.textContent = "Ошибка загрузки: " + err.message;
        });
    }
});
