document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded");

  let mediaRecorder;
  let audioChunks = [];
  let stream; // To hold the audio stream for stopping tracks
  let videoStream; // To hold the video stream for stopping tracks
  const totalQuestions = 5; // Total number of questions (matches get_sql_questions() in app.py)

  // Function to start the video feed
  async function startVideoFeed() {
    try {
      let videoElement = document.getElementById("video-feed");
      if (!videoElement) {
        console.warn("Video element not found, creating dynamically");
        videoElement = document.createElement("video");
        videoElement.id = "video-feed";
        videoElement.autoplay = true;
        videoElement.playsInline = true;
        videoElement.style.width = "640px";
        videoElement.style.height = "480px";
        videoElement.style.border = "3px solid #ff0000";
        videoElement.style.borderRadius = "10px";
        videoElement.style.boxShadow = "0 0 20px rgba(255, 0, 0, 0.5)";
        videoElement.style.animation = "recording-border 1.5s infinite";
        document.getElementById("video-container").appendChild(videoElement);
        if (!document.getElementById("video-feed")) {
          throw new Error("Failed to create video element dynamically");
        }
      }
      // Check if videoStream already exists and stop it to avoid conflicts
      if (videoStream) {
        videoStream.getTracks().forEach((track) => track.stop());
        videoStream = null;
      }
      console.log("Requesting webcam access...");
      videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
      console.log(
        "Webcam access granted, assigning stream to video element..."
      );
      videoElement.srcObject = videoStream;
      document.getElementById("video-container").style.display = "block"; // Show the video container
      console.log("Video feed started successfully");
    } catch (error) {
      console.error("Error accessing webcam:", error);
      alert("Error: Failed to access webcam. " + error.message);
      // Provide additional guidance for common errors
      if (error.name === "NotAllowedError") {
        alert(
          "Please grant permission to access your webcam in your browser settings."
        );
      } else if (error.name === "NotFoundError") {
        alert(
          "No webcam found. Please ensure a webcam is connected and available."
        );
      }
    }
  }

  // Function to stop the video feed
  function stopVideoFeed() {
    try {
      if (videoStream) {
        videoStream.getTracks().forEach((track) => track.stop());
        const videoElement = document.getElementById("video-feed");
        if (videoElement) {
          videoElement.srcObject = null;
          document.getElementById("video-container").style.display = "none"; // Hide the video container
        }
        videoStream = null;
        console.log("Video feed stopped successfully");
      }
    } catch (error) {
      console.error("Error stopping video feed:", error);
    }
  }

  // Start Interview
  document
    .getElementById("start-interview")
    .addEventListener("click", async () => {
      try {
        const response = await fetch("/start_interview", { method: "POST" });
        const data = await response.json();
        if (data.audio_url) {
          const audio = new Audio(data.audio_url);
          audio.play();
          document.getElementById("record-answer").disabled = false;
          document.getElementById("start-interview").disabled = true;
          document.getElementById("next-question").disabled = true;
          document.getElementById("submit-interview").disabled = true;
          // Start the video feed when the interview begins
          await startVideoFeed();
        } else {
          alert("Error: Failed to start interview. " + (data.message || ""));
        }
      } catch (error) {
        alert("Error: Failed to start interview. " + error.message);
      }
    });

  // Record Answer
  document
    .getElementById("record-answer")
    .addEventListener("click", async () => {
      const recordButton = document.getElementById("record-answer");
      if (!mediaRecorder || mediaRecorder.state === "inactive") {
        try {
          // Start recording
          stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          // Try different mimeTypes if webm doesn't work
          const mimeType = MediaRecorder.isTypeSupported("audio/webm")
            ? "audio/webm"
            : MediaRecorder.isTypeSupported("audio/wav")
            ? "audio/wav"
            : "audio/mp3";
          mediaRecorder = new MediaRecorder(stream, { mimeType: mimeType });
          audioChunks = [];
          mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
              audioChunks.push(event.data);
            }
          };
          mediaRecorder.start();
          recordButton.textContent = "Stop Recording";
          // Disable both buttons while recording
          document.getElementById("next-question").disabled = true;
          document.getElementById("submit-interview").disabled = true;
        } catch (error) {
          alert("Error: Failed to start recording. " + error.message);
        }
      } else {
        // Stop recording
        mediaRecorder.stop();
        mediaRecorder.onstop = async () => {
          // Stop the audio stream to release the microphone
          stream.getTracks().forEach((track) => track.stop());

          const audioBlob = new Blob(audioChunks, {
            type: mediaRecorder.mimeType,
          });
          console.log("Audio Blob Size:", audioBlob.size); // Debug: Check blob size
          console.log("MimeType:", mediaRecorder.mimeType); // Debug: Check mimeType
          if (audioBlob.size === 0) {
            alert("Error: Recorded audio is empty.");
            recordButton.textContent = "Record Answer";
            return;
          }

          const formData = new FormData();
          const fileExtension = mediaRecorder.mimeType.includes("webm")
            ? "webm"
            : mediaRecorder.mimeType.includes("wav")
            ? "wav"
            : "mp3";
          formData.append("audio", audioBlob, `answer.${fileExtension}`);

          try {
            const response = await fetch("/submit_answer", {
              method: "POST",
              body: formData,
            });
            const result = await response.json();
            if (result.status === "recorded") {
              // Enable the appropriate button based on visibility
              const nextButton = document.getElementById("next-question");
              const submitButton = document.getElementById("submit-interview");
              if (submitButton.style.display === "inline-block") {
                submitButton.disabled = false; // Enable Submit button
              } else {
                nextButton.disabled = false; // Enable Next Question button
              }
              document.getElementById("record-answer").disabled = true;
            } else {
              alert(
                "Error: Failed to submit answer. " + (result.message || "")
              );
            }
          } catch (error) {
            alert("Error: Failed to submit answer. " + error.message);
          }
          recordButton.textContent = "Record Answer";
        };
      }
    });

  // Next Question
  document
    .getElementById("next-question")
    .addEventListener("click", async () => {
      try {
        const response = await fetch("/next_question", { method: "POST" });
        const data = await response.json();
        if (data.status === "complete") {
          // Display table with evaluation
          const table = document.createElement("table");
          table.innerHTML =
            "<tr><th>Timestamp</th><th>Question</th><th>Answer</th><th>Score</th><th>Feedback</th></tr>";
          data.table.forEach((row) => {
            table.innerHTML += (
              <tr>
                <td>${row.timestamp}</td>
                <td>${row.question}</td>
                <td>${row.answer}</td>
                <td>${row.score}/100</td>
                <td>${row.feedback}</td>
              </tr>
            );
          });
          document.body.appendChild(table);
          document.getElementById("start-interview").disabled = false;
          document.getElementById("record-answer").disabled = true;
          document.getElementById("next-question").disabled = true;
          document.getElementById("submit-interview").style.display = "none"; // Hide Submit button
          document.getElementById("next-question").style.display =
            "inline-block"; // Show Next Question button
          // Stop the video feed when the interview is complete
          stopVideoFeed();
        } else {
          const audio = new Audio(data.audio_url);
          audio.play();
          // Check if this is the last question
          if (data.question_number === totalQuestions) {
            document.getElementById("next-question").style.display = "none"; // Hide Next Question button
            document.getElementById("submit-interview").style.display =
              "inline-block"; // Show Submit button
            document.getElementById("submit-interview").disabled = true; // Disable until recording is submitted
          } else {
            document.getElementById("next-question").disabled = true;
          }
          document.getElementById("record-answer").disabled = false;
        }
      } catch (error) {
        alert(
          "Error: Failed to load next question or submit interview. " +
            error.message
        );
      }
    });

  // Submit Interview
  document
    .getElementById("submit-interview")
    .addEventListener("click", async () => {
      try {
        const response = await fetch("/next_question", { method: "POST" });
        const data = await response.json();
        if (data.status === "complete") {
          // Display table with evaluation
          const table = document.createElement("table");
          table.innerHTML =
            "<tr><th>Timestamp</th><th>Question</th><th>Answer</th><th>Score</th><th>Feedback</th></tr>";
          data.table.forEach((row) => {
            table.innerHTML += (
              <tr>
                <td>${row.timestamp}</td>
                <td>${row.question}</td>
                <td>${row.answer}</td>
                <td>${row.score}/100</td>
                <td>${row.feedback}</td>
              </tr>
            );
          });
          document.body.appendChild(table);
          document.getElementById("start-interview").disabled = false;
          document.getElementById("record-answer").disabled = true;
          document.getElementById("next-question").disabled = true;
          document.getElementById("submit-interview").style.display = "none"; // Hide Submit button
          document.getElementById("next-question").style.display =
            "inline-block"; // Show Next Question button
          // Stop the video feed when the interview is complete
          stopVideoFeed();
        } else {
          const audio = new Audio(data.audio_url);
          audio.play();
          // Check if this is the last question
          if (data.question_number === totalQuestions) {
            document.getElementById("next-question").style.display = "none"; // Hide Next Question button
            document.getElementById("submit-interview").style.display =
              "inline-block"; // Show Submit button
            document.getElementById("submit-interview").disabled = true; // Disable until recording is submitted
          } else {
            document.getElementById("next-question").disabled = true;
          }
          document.getElementById("record-answer").disabled = false;
        }
      } catch (error) {
        alert(
          "Error: Failed to load next question or submit interview. " +
            error.message
        );
      }
    });
});
