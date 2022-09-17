// =========== Getting references to manipulate DOM ========== //
let files = [],
    form = document.querySelector('form'),
    container = document.querySelector('.image__container'),
    text = document.querySelector('.drop-text'),
    input = document.querySelector('.drop__file-upload input'),
    result = document.getElementById('result');

// =========== Input Change Event ========== //
input.addEventListener('change', ()=>{
    let file = input.files;
    if(files.length == 1)
    {
        files.pop();
    }
    
    files.push(file[0]);
    form.reset();   
    showImages();
})

// =========== Fuction to Calculate size of Image in MB/KB ========== //
function calcSize(size)
{
    if(Math.floor(size/1024/1000) == 0)
        return Math.floor(size/1024)+' kb';
    else
        return Math.floor(size/1024/1000)+' mb';
}

// =========== Function to create a new container to show uploaded IMAGE Dynamically ========== //
const showImages = () => {
    let images = '';
    files.forEach((e, i) =>{
        images += `<div class="uploaded__image">
        <img src="${URL.createObjectURL(e)}" alt="selected image">
        <div class="img_details">
            <h4 class="title">${e.name}</h4>
            <p>${calcSize(e.size)}</p>
            <button onclick="_handleImageLoaded()" class="submit_btn">Upload</button>
        </div>
        <span onclick="delImage(${i})"></span>
    </div>`
    })

    // if(files.length === 0)
    //     result.classList.remove('result')
    // else
    //     result.classList.add('result');

    container.innerHTML = images;

    if(files.length != 0)
    {
        let button = document.querySelector('button');

        button.addEventListener('click', () => {
            let form = new FormData();
            files.forEach((e, i) => form.append(`file[${i}]`, e));
            // console.log("clicked");
            button.disabled = true
        })
    }
}

// =========== Fuction to delete uploaded image ========== //
const delImage = index =>{
    files.splice(index, 1);

    if(files.length === 0)
        result.classList.remove('result')
    else
        result.classList.add('result');

    showImages();
}

// =========== To handle image when Draged Over ========== //
form.addEventListener('dragover', e =>{
    e.preventDefault();

    // form.classList.add('dragover');
    text.classList.add('dragover');
    text.innerHTML = "Drop images here";
})

// =========== To handle image when Draged Out of input ========== //
form.addEventListener('dragleave', e =>{
    e.preventDefault();

    // form.classList.remove('dragover');
    text.classList.remove('dragover');
    text.innerHTML = 'Drag & drop here OR click to <strong>Browse</strong>';
})

// =========== To handle image when Dropped on input ========== //
form.addEventListener('drop', e =>{
    e.preventDefault();

    // form.classList.remove('dragover');
    text.classList.remove('dragover');
    text.innerHTML = 'Drag & drop here OR click to <strong>Browse</strong>';
    
    let file = e.dataTransfer.files;
    if(files.length == 1)
    {
        files.pop();
    }
    
    files.push(file[0]);
    form.reset();

    showImages();

    const f = files[0];
    const reader = new FileReader();
    reader.readAsDataURL(f);
    reader.addEventListener("load", ()=>{
        // console.log(reader.result);
        fileData = reader.result;
    })
})


// API calling //
// =========== Conversion of string to Base64 ========== //
let fileData = '';
input.addEventListener("change", e=> {
    const f = files[0];
    const reader = new FileReader();
    reader.readAsDataURL(f);
    reader.addEventListener("load", ()=>{
        // console.log(reader.result);
        fileData = reader.result;
    })
})

// =========== Sending UPLOADED IMAGE(Base64) and CATEGORY to SERVER and Receving RESPONSE ========== //
function _handleImageLoaded() {
    //let human_model = document.querySelector('.dropdown select').value;
    let form = new FormData();
    form.append('file', fileData);
    //form.append('human_model', human_model);
    // console.log(fileData);
    // console.log(form);
    // console.log(fileData);
    // console.log(fileData.length);
    // console.log(human_model);
    // console.log(human_model.length);

    fetch("https://noiceuploader.pagekite.me//file-upload", {
        method: "post",
        mode: "no-cors",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, DELETE, PUT',
            'Authorization': 'Bearer key',
        },
        body: form,
    }).then(data => data.json())
        .then(function (response) {
            if(response.output)
                return response.output;
            else
                return "Empty response";
        })
        .then(function (data) {
            data.forEach(()=> console.log(data))
            data.forEach((elem)=>{
                //let images = `<img class="fetched__images" src="${data}" alt="result-image">`;
                //console.log(images);
                //let next = document.getElementById("result");
                //console.log(next);
                //next.innerHTML = images;
                let image = new Image();
                image.src = "data:image/png;base64,"+elem;
                document.getElementById('result').appendChild(image);
            })
            // let next = document.querySelector("#fetched__image");
            // next.src = "data:images/png;base64,"+data;
        })
        .catch((error) => console.error("Error:", error));

        if(files.length === 0)
            result.classList.remove('result')
        else
            result.classList.add('result');
}


// =========== Parallax Mousemove ========== //
document.addEventListener('mousemove', (e)=>{
    let heading = document.querySelector('.hero__heading');
    let moving_value = heading.getAttribute('data-value');
    let x = (e.clientX * moving_value)/230;
    let y = (e.clientY * moving_value)/230;

    heading.style.transform = "translateX(" + x + "px) translateY(" + y + "px";
});