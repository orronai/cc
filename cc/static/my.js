function escapeUnicode(str) {
  // Thanks to https://stackoverflow.com/a/45315988
  const json = JSON.stringify(str);
  return json.replace(/[\u007F-\uFFFF]/g, (chr) => {
    const step1 = chr.charCodeAt(0).toString(16);
    const step2 = `0000${step1}`.substr(-4);
    return `\\u${step2}`;
  });
}

function trackDateElement(dateElement) {
  dateElement.addEventListener('focus', () => {
    dateElement.type = 'date';
  });
  dateElement.addEventListener('blur', () => {
    dateElement.type = 'text';
  });
}

function setMaxDateToday(dateElement) {
  const today = new Date().toISOString().split('T')[0];
  dateElement.setAttribute('max', today);
}

function addGraph(graphDetails, graphElement) {
  graphElement.innerHTML = `<img src="data:image/png;base64,${graphDetails.graph}">`;
  if (window.resultTitle.classList.contains('d-none')) {
    window.resultTitle.classList.remove('d-none');
  }
}

function trackCreateGraph(formElement) {
  formElement.addEventListener('submit', (e) => {
    e.preventDefault();
    const serializeData = new URLSearchParams(Array.from(new FormData(formElement))).toString();
    const xhr = new XMLHttpRequest();
    const url = `/graph?${serializeData}`;
    xhr.open('GET', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.responseType = 'json';
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          addGraph(JSON.parse(escapeUnicode(xhr.response)), document.getElementById('graph'));
        } else {
          console.log(xhr.status);
        }
      }
    };

    xhr.send('');
  });
}


window.addEventListener('load', () => {
  const datesElements = document.getElementsByClassName('dates');
  window.resultTitle = document.getElementById('result-title');
  Array.from(datesElements).forEach((date) => {
    trackDateElement(date);
    setMaxDateToday(date);
  });
  trackCreateGraph(document.getElementById('search-form'));
});
