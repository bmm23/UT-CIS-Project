console.log('content.js running')


function linkScraper() {
    document.querySelector("tr").remove()
    let table = document.querySelectorAll("tr")
    let tableTags = []

    table.forEach(element =>
         tableTags.push(element.querySelector("td").querySelector("a").href))
    return tableTags

}

function nextPageButtonClick() {
    let buttons = document.querySelectorAll("input")
    let button = buttons[buttons.length - 1]

    setTimeout(() => {button.click()}, 1500);
}


function exportArray(arr) {
    var _myArray = JSON.stringify(arr , null, 4); //indentation in json format, human readable

    var vLink = document.createElement('a'),
    vBlob = new Blob([_myArray], {type: "octet/stream"}),
    vName = 'saver.json',
    vUrl = window.URL.createObjectURL(vBlob);
    vLink.setAttribute('href', vUrl);
    vLink.setAttribute('download', vName );
    vLink.click();
    console.log('saved array')
}
let links = linkScraper()

//exportArray(links)

//nextPageButtonClick()

