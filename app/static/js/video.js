document.addEventListener("DOMContentLoaded", function () {
    const videoElement = document.getElementById("camera-stream");
    const predictButton = document.getElementById("predict-button");

    let videoStream;
    let recordedChunks = [];
    let countdownInterval;
    let isCameraActive = false;

    // Function to start the camera stream
    function startCameraStream() {
        if (navigator.mediaDevices.getUserMedia) {
            const constraints = {
                video: { width: { ideal: 1280 }, height: { ideal: 720 } }
            };
            navigator.mediaDevices.getUserMedia(constraints)
                .then(function (stream) {
                    videoStream = stream;
                    videoElement.srcObject = stream;
                })
                .catch(function (error) {
                    console.error("Error accessing the camera: ", error);
                });
        } else {
            console.error("getUserMedia is not supported by this browser.");
        }

        isCameraActive = true;
    }

    // Function to stop the camera stream
    function stopCameraStream() {
        if (videoStream) {
            videoStream.getTracks().forEach(track => track.stop());
        }

        isCameraActive = false;
    }

    // Function to handle the video stream data and send it to the server for processing
    function captureAndProcessVideo() {
        recordedChunks = [];
        const mediaRecorder = new MediaRecorder(videoStream);

        mediaRecorder.ondataavailable = function (event) {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = function () {
            const blob = new Blob(recordedChunks, {type: "video/webm"});
            const formData = new FormData();
            formData.append("video", blob);

            fetch("/process_video", {
                method: "POST",
                body: formData,
            })
            .then((response) => response.json())
            .then((data) => {
                // Handle the video classification result (data.result)
                console.log("Video classification result: ", data.result);
            })
            .catch((error) => console.error("Error during video classification: ", error));
        };

        // Countdown for video recording
        const countdownElement = document.getElementById("countdown");
        const countdownDuration = 3; // Set the countdown duration in seconds
        let countdownTime = countdownDuration;

        countdownInterval = setInterval(function () {
            if (countdownTime <= 0) {
                clearInterval(countdownInterval);
                countdownElement.textContent = ""; // Clear the countdown text
                mediaRecorder.stop();
                stopCameraStream(); // Stop the camera stream after recording
            } else {
                countdownElement.textContent = countdownTime + " s";
                countdownTime--;
            }
        }, 1000);

        mediaRecorder.start();
    }


    // Function to start the countdown
    function startCountdown(duration) {
        let remainingTime = duration;
        const countdownElement = document.getElementById("countdown");

        countdownInterval = setInterval(function () {
            if (remainingTime <= 0) {
                clearInterval(countdownInterval);
                countdownElement.textContent = ""; // Clear the countdown text
                captureAndProcessVideo();
            } else {
                countdownElement.textContent = remainingTime + " s";
                remainingTime--;
            }
        }, 1000);
    }

    // Function to update the result dynamically
    function updateResult() {
        if (isCameraActive) {
            return;
        }

        fetch("/get_result")
            .then((response) => response.json())
            .then((data) => {
                // Update the result in the DOM
                const resultElement = document.getElementById("result");
                resultElement.textContent = data.result;
            })
            .catch((error) => console.error("Error fetching result: ", error));
    }

    setInterval(updateResult, 1000);

    // Event listener for the "Predict" button
    predictButton.addEventListener("click", () => {
        startCameraStream();
        startCountdown(3);
    });

    // Stop the camera stream when leaving the page
    window.onbeforeunload = stopCameraStream;
});