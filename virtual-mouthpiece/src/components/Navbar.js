import React from "react"

export default function Navbar() {

    return (
        <header>
            <nav>
                <ul className="navItems">
                    <li className="titleLi">
                        <h1 className="title">Virtual Mouthpiece</h1>
                        <h3 className="subtitle">Billboard Updater</h3>
                    </li>
                    <li>
                        <button className="redButton">Create Slideshow</button></li>
                        <li><button className="blueButton">⚙</button>
                    </li>
                </ul>
            </nav>
        </header>
    )
}
