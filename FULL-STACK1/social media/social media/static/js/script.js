// ==========================================
// DELETE POST CONFIRMATION
// ==========================================

function confirmDelete() {
    return confirm("Are you sure you want to delete this post?");
}


// ==========================================
// FOCUS COMMENT INPUT
// ==========================================

function focusComment(postId) {

    const commentInput = document.getElementById(
        "comment-" + postId
    );

    if (commentInput) {
        commentInput.focus();
    }
}


// ==========================================
// POST IMAGE PREVIEW
// ==========================================

function previewPostImage(event) {

    const file = event.target.files[0];

    const previewContainer =
        document.getElementById(
            "imagePreviewContainer"
        );

    const previewImage =
        document.getElementById(
            "imagePreview"
        );


    if (!file) {

        previewContainer.style.display = "none";

        previewImage.src = "";

        return;
    }


    const reader = new FileReader();


    reader.onload = function (e) {

        previewImage.src = e.target.result;

        previewContainer.style.display = "block";

    };


    reader.readAsDataURL(file);
}


// ==========================================
// AUTO HIDE DJANGO MESSAGES
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const messages =
            document.querySelectorAll(
                ".message"
            );


        if (messages.length > 0) {

            setTimeout(function () {

                messages.forEach(function (message) {

                    message.style.transition =
                        "opacity 0.5s ease";

                    message.style.opacity = "0";


                    setTimeout(function () {

                        message.remove();

                    }, 500);

                });

            }, 3500);

        }

    }
);


// ==========================================
// PREVENT EMPTY SEARCH SPACES
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const searchForms =
            document.querySelectorAll(
                'form[action*="search"]'
            );


        searchForms.forEach(function (form) {

            form.addEventListener(
                "submit",
                function (event) {

                    const input =
                        form.querySelector(
                            'input[name="q"]'
                        );


                    if (input) {

                        input.value =
                            input.value.trim();


                        if (
                            input.value.length === 0
                        ) {

                            event.preventDefault();

                            input.focus();

                        }

                    }

                }
            );

        });

    }
);