import React, { useState, useEffect } from "react";
import axios from "axios";

function ImageUpload({ setData, setErr }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [image, setImage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const threshold = 0.5;

  const sendFile = async () => {
    if (image) {
      let formData = new FormData();
      formData.append("file", selectedFile);
      try {
        let res = await axios.post(process.env.REACT_APP_API_URL, formData);
        if (res.status === 200) {
          console.log(res.data);
          if (res.data.confidence < threshold) {
            setData({ class: "Default", confidence: "100" });
            clearData();
            setErr(true);
          } else {
            setData(res.data);
          }
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
      setIsLoading(false);
    }
  };

  const clearData = () => {
    setData({ class: "Default", confidence: "100" });
    setImage(false);
    setSelectedFile(null);
  };

  const onSelectFile = (event) => {
    const file = event.target.files[0];
    if (!file) {
      clearData();
      return;
    }
    setSelectedFile(file);
    setImage(true);
  };

  useEffect(() => {
    if (!selectedFile) {
      return;
    }
    setIsLoading(true);
    setErr(false);
    sendFile();
  }, [selectedFile]);

  return (
    <>
      <div className="col-12 col-sm-3 ">
        <div class="input-group mb-3 ps-3 ">
          <input
            type="file"
            class="form-control"
            accept="image/*"
            onChange={onSelectFile}
            id="imageInput"
          />
          <label class="input-group-text">Upload</label>
        </div>
      </div>

      {isLoading && <p>Loading...</p>}
      <div className="col-12 col-sm-2">
        <button className="btn btn-dark" onClick={clearData}>
          Clear
        </button>
      </div>
    </>
  );
}

export default ImageUpload;
