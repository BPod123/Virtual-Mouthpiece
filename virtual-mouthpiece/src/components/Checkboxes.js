import React from "react"

export default function Checkboxes() {

    return (
        <div>
            <div className="top"></div>
            <label className="container">Front Board
                <input type="checkbox"></input>
                <span className="checkmark"></span>
            </label>
            <label className="container">Airstrip Board
                <input type="checkbox"></input>
                <span className="checkmark"></span>
            </label>
            <div className="bottom"></div>
        </div>
    )

}