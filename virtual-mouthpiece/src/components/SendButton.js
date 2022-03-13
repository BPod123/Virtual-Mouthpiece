import React from "react";
import toast, { Toaster } from "react-hot-toast";

export default function SendButton(props) {
  const image = props.image;
  return (
    <button
      className="sendButton"
      onClick={() => {
        console.log("billboard clicked");
        const fd = new FormData();
        image && console.log(image.name);
        image && fd.append("file", image);
        toast.promise(
          fetch("/flask/hello", {
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
