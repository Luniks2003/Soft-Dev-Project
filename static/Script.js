document.addEventListener('DOMContentLoaded', function() {
    const selectImage = document.querySelector('.select-image')
    const inputFile = document.querySelector('#file')
    const uploadFile = document.querySelector('.upload-image')
    const uploadFileForm = document.querySelector('#upload')
    const imgArea = document.querySelector('.img-area')
    const popup = document.querySelector('.popup')
    const popupImg = document.querySelector('.popup img')
    const closeBtn = document.querySelector('.popup .close')
    const downloadFileForm = document.querySelector('#download')
    const downloadFile = document.querySelector('.download-image')

    // Event listener for when the 'Select Image' button is clicked
    selectImage.addEventListener('click', function () {
        // Trigger a click event on the inputFile element to open the file picker
        inputFile.click();
    })  

    downloadFile.addEventListener('click', () =>{
        downloadFileForm.click();
    })

    // Event listener for when the 'Upload Image' button is clicked
    uploadFile.addEventListener('click', () => {
        uploadFileForm.click();
    })
    // Event listener for when an image is selected
    inputFile.addEventListener('change', function () {
        const image = this.files[0];
        if (image.size < 10000000) {
            const reader = new FileReader();
            reader.onload = () => {
                const imgUrl = reader.result;
                const img = document.createElement('img');
                img.src = imgUrl;
                imgArea.innerHTML = ''; // Clear previous image
                imgArea.appendChild(img);
                imgArea.classList.add('active');
                imgArea.dataset.img = image.name;

                // Add a click event listener to the displayed image
                img.onclick = () => {
                    // Display the popup when the image is clicked
                    popup.style.display = 'block';
                    // Set the source of the popup image to the source of the clicked image
                    popupImg.src = img.src;
                };
            };
            reader.readAsDataURL(image);
        } else {
            alert("Image size more than 10MB");
        }
    });

    // Event listener for when the close button of the popup is clicked
    closeBtn.addEventListener('click', function() {
        // Hide the popup when the close button is clicked
        popup.style.display = 'none';
    });
});

