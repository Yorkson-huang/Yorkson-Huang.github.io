function toggleCitation(id) {
  var popup = document.getElementById(id);
  var allPopups = document.getElementsByClassName('citation-popup');
  
  // Close all other popups
  for(var i = 0; i < allPopups.length; i++) {
    if(allPopups[i].id !== id) {
      allPopups[i].style.display = 'none';
    }
  }
  
  // Toggle this popup
  if(popup.style.display === 'block') {
    popup.style.display = 'none';
  } else {
    popup.style.display = 'block';
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(function() {
    var lang = document.documentElement.lang || 'en';
    if (lang === 'zh') {
      alert('引用已复制到剪贴板！');
    } else {
      alert('Citation copied to clipboard!');
    }
  }, function(err) {
    console.error('Could not copy text: ', err);
  });
}

function toggleThesis(id) {
  var abstract = document.getElementById(id);
  if(abstract.style.display === 'block') {
    abstract.style.display = 'none';
  } else {
    abstract.style.display = 'block';
  }
}

// Close popups when clicking outside
window.onclick = function(event) {
  if (!event.target.matches('.citation-btn') && !event.target.matches('.citation-popup') && !event.target.matches('.citation-format')) {
    var popups = document.getElementsByClassName('citation-popup');
    for(var i = 0; i < popups.length; i++) {
      popups[i].style.display = 'none';
    }
  }
} 
