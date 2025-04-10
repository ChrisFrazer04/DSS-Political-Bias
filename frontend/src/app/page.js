"use client"

import Image from "next/image";
//import styles from "./page.module.css";
import ArticleBox from "./components/text_box";

export default function Home() {
  return (
    <div className="container">
        <h1>Bias Analysis Tool</h1>
        <textarea id="inputText" placeholder="Paste article text here..."></textarea>
        <ArticleBox/>
        <div class="buttons">
            <button id="checkBias">Check Bias</button>
            <button id="highlightWords">Highlight Bias Words</button>
        </div>
        
        <div class="results">
            <h2>Results:</h2>
            <p><strong>Leans:</strong> <span id="biasLeaning">N/A</span></p>
            <p><strong>Accuracy/Confidence:</strong> <span id="confidence">N/A</span></p>
            <h3>Keywords:</h3>
            <div id="keywords"></div>
            <h3>Key Biases:</h3>
            <ul id="keyBiases"></ul>
        </div>
    </div>
  );
}