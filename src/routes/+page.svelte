<script>
    import { PDFDocument } from 'pdf-lib'

    let dz; 
    let startInput; 
    let endInput; 
    let sliceButton; 
    let fileInput; 

    let startValue = undefined;
    let endValue = undefined;
    let files = undefined;

    function prevent(event) {
        event.preventDefault()
    }

    function handleDrop(event) {
        event.preventDefault();

        if (files == undefined) {
            files = event.dataTransfer.files[0];
            if (files.length > 0) {
                handleFile(files[0]);
            }
        }
    }

    function processInputs() {
        if (files == undefined) {
            files = fileInput.files[0];  
            console.log(files) 
        }
        startValue = parseInt(startInput.value, 10);
        endValue = parseInt(endInput.value, 10);
    }

    function handleFile(file) {
        if (file && file.type === 'application/pdf') {
            console.log('File:', file);
        } else {
            alert('Please drop a valid PDF file.');
        }
    }

    async function mainProcess () {
        processInputs();

        if (files == undefined) {
            alert("Kindly upload a file!")
        }
        if (startValue == undefined || endValue == undefined) {
            alert("Kindly fill in the input values!")
        }
        
        let Res;
        const blob = new Blob([files], {type: 'application/pdf'})
        Res = await blob.arrayBuffer();
        
        const pdfDoc = await PDFDocument.load(Res); 
        const newDoc = await PDFDocument.create();

        for (let i=startValue-1; i < endValue; i++) {
            let [page] = await newDoc.copyPages(pdfDoc, [i])
            newDoc.addPage(page);
        }

        const pdfBytes = await newDoc.save();

        let link = document.createElement('a');
        link.href = window.URL.createObjectURL(new Blob([pdfBytes]));
        link.download = 'newPDF.pdf';
        link.click();
        alert("Downloaded!")
        window.location.href = window.location.href
    }
</script>

<header>
    <h1>
        Pdf S<span>/</span>icer
    </h1>
</header>
<main>
    <div id="dropZone" bind:this={dz} on:drop={handleDrop} on:dragover={prevent} on:dragleave={prevent} role="application">
        Drop Here
    </div>
    <div class="file-input">
        <input type="file" id="file" class="file" accept="application/pdf" bind:this={fileInput}>
        <label for="file">Select fil</label>
        <input id="start" type="number" name="startPage" placeholder="Start" bind:this={startInput}>
        <input id="end" type="number" name="endPage" placeholder="End" bind:this={endInput}>
    </div>
</main>
<div id="b"><button id="slice" on:click={mainProcess} bind:this={sliceButton}>Slice and Download</button></div>

<style>
    :global(body) {
    background-color: rgb(51,51,51);
    }
    h1 {
        color: white;
    }
    span {
        color: grey;
        font-weight: bolder;
    }
    header {
        text-align: center;
        font-size:x-large;
    }
    main {
        margin-top: 15%;
        display: flex;
        justify-content: center;
    }

    .file {
        height: 0.1px;
        position: absolute;
        opacity: 0;
        width: 0.1px;
    }
    .file-input label, #start, #end {
        display: block;
        position: relative;
        width: 120px;
        height: 40px;
        margin-left: 10%;
        border: 1px solid grey;
        border-radius: 25px;
        background-color: rgb(41, 41, 41);
        box-shadow: 0 4px 7px rgba(0, 0, 0, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgb(184, 183, 183);
        font-weight: bold;
        cursor: pointer;
        transition: transform .2s ease-out;
        margin-top: 10%;
    }
    #start,     #end {
        text-align: center;
    }
    #start:focus,   #end:focus{
        outline: none;
    }
    #dropZone {
        align-items: center;
        justify-content: center;
        height: 20vh;
        width: 20vw;
        background-color: rgb(41, 41, 41);
        border: 1px solid grey;
        color: grey;
        display: flex;
    }
    #b {
        align-items: center;
        justify-content: center;
        display: flex;
    }
    #slice {
        width: 240px;
        height: 40px;
        background-color: inherit;
        outline: none;
        border: 1px solid grey;
        color: rgb(187, 187, 187);
        margin-top: 5%;
    }
    #slice:hover {
        color: inherit;
        cursor: pointer;
        background-color: rgb(187, 187, 187);
    }
    @media only screen and (max-width: 768px) {
        main {
            margin-top: 50%;
        }
    }
</style>