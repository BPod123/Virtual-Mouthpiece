import React from "react"

export default function Navbar() {

    return (
        <header>
            <nav>
                <h3 className="title">Virtual Mouthpiece - Billboard Updater</h3>
                <ul className="navItems">
                    <li><button className="redButton">Create Slideshow</button></li>
                    <li><button className="blueButton">⚙</button></li>
                </ul>
            </nav>
        </header>
    )
}
