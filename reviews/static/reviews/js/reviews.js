
window.onload = function () {

    const editButton = document.getElementById("edit-button");
    const reviewText = document.getElementById("id_body");
    const reviewForm = document.getElementById("review-form");
    const submitButton = document.getElementById("submit-button");

    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButton = document.getElementById("delete-button");
    const deleteConfirm = document.getElementById("deleteConfirm");

    if (editButton) {
        editButton.addEventListener("click", (e) => {
            let reviewId = e.target.getAttribute("review_id");
            let productId = e.target.getAttribute("product_id")
            let reviewContent = document.getElementById(`review${reviewId}`).innerText;
            reviewText.value = reviewContent;
            submitButton.innerText = "Update";
            reviewForm.setAttribute("action", `reviews/${productId}/edit_review/${reviewId}`);
        });

    }

    if (deleteButton) {
        deleteButton.addEventListener("click", (e) => {
          let reviewId = e.target.getAttribute("review_id");
          let productId = e.target.getAttribute("product_id");
          deleteConfirm.href = `reviews/${productId}/delete_review/${reviewId}`;
          deleteModal.show();
        });
      }

}


