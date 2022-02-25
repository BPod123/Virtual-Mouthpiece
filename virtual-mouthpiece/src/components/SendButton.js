import React from "react"

export default function SendButton(props) {
    const image = props.image;
    return (
        <button
            className="sendButton"
            onClick={() => {
                const fd = new FormData();
                image && console.log(image.name)
                image && fd.append('file', image)
                fetch('/flask/hello', {
                method: 'POST',
                body: fd
                }).then(resp => {
                resp.json().then(data => {console.log(data)})
                })
            }}
        >
            Send to Billboard
        </button>
    )

}
