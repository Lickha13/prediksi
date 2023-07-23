function toggleSidebar() {
  let elm = document.getElementById('sidebar')

  if (elm.classList.contains('show')) {
     elm.classList.remove('show');
  } else {
     elm.classList.add('show');
  }
}

function innerHtml(target, html) {
  document.getElementById(target).innerHTML = html;
}

function appendHtml(target, html) {
  document.getElementById(target).innerHTML += html;
}

function percentage(item, total) {
  let temp = (item / total) * 100;
  return parseFloat(temp).toFixed(2);
}

function detectSpecialWord(full_text, word) {
  return full_text.replace(/(?:^|)depresi(?:$|)/g, `<span class="fw-bold">${word}</span>`)
}

function escapeNewLine(full_text) {
  return full_text.replace(/(\r\n|\r|\n)/g, "<br/>")
}
