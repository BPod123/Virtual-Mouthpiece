import React from "react";
import toast from "react-hot-toast";

export default function SendButton(props) {
  const { image, checks, imageList } = props;
  return (
    <button
      className="sendButton"
      onClick={() => {
        console.log("billboard clicked");
        const fd = new FormData();
        imageList.length !== 0 && console.log(imageList);
        image && fd.append("file", image);
        checks && fd.append("board", checks['billboard']);
        toast.promise(
          fetch("/flask/upload", {
        //   fetch("http://127.0.0.1:5000/flask/upload", {
            method: "POST",
            body: fd,
          }).then((resp) => {
            resp.json().then((data) => {
              console.log(data);
            });
          }),
          {
            loading: "Sending...",
            success: <b>Sent!</b>,
            error: <b>ERROR! Could not send.</b>,
          }
        );
      }}
    >
      Send to Billboard
    </button>
  );
}
