function requestURL (url, handler) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                handler(xhr.responseText);
            }
        }
    };
    xhr.send(null);
}

/**
 * @param {String} HTML representing a single element.
 * @param {Boolean} flag representing whether or not to trim input whitespace, defaults to true.
 * @return {Element | HTMLCollection | null}
 */
function fromHTML(html, trim = true) {
  // Process the HTML string.
  html = trim ? html.trim() : html;
  if (!html) return null;

  // Then set up a new template element.
  const template = document.createElement('template');
  template.innerHTML = html;
  const result = template.content.children;

  // Then return either an HTMLElement or HTMLCollection,
  // based on whether the input HTML had one or more roots.
  if (result.length === 1) return result[0];
  return result;
}

function wrapinli(el) {
	var wrapper = document.createElement('li');
    el.parentNode.insertBefore(wrapper, el);
    wrapper.appendChild(el);
    return wrapper;
}
function postnavbarHandlerJson(creatorsText)
{
    var toggler = document.getElementById("navbar_creator_list");
    var crlink = document.getElementById("creator_link");
    var creators = JSON.parse(creatorsText);
    
    toggler.innerHTML = "";
    console.log(creators);
    console.log(creators);
	for (var i = 0; i < creators.length; i++) {
		var atag = document.createElement("a");
		atag.classList.add("dropdown-item");
		atag.classList.add("link");
		atag.innerText = creators[i].name;
	   	atag.setAttribute('href',crlink.getAttribute('href')+creators[i].id);
        toggler.appendChild(atag.cloneNode(true));
	}
}
function postnavbarHandlerJsonCreations(creatorsText)
{
    var toggler = document.getElementById("navbar_creation_list");
    var crlink = document.getElementById("creation_link");
	var creations = JSON.parse(creatorsText);
    
    console.log(creations);
    toggler.innerHTML = "";
	for (var i = 0; i < creations.length; i++) {
		var atag = document.createElement("a");
		atag.classList.add("dropdown-item");
		atag.classList.add("link");
		atag.innerText = creations[i].name;
		let lnk = crlink.getAttribute('href');
		lnk = lnk.replace('crtor_id', creations[i].creator_id);
		lnk = lnk.replace('crtion_id', creations[i].id);
	   	atag.setAttribute('href', lnk);
        toggler.appendChild(atag.cloneNode(true));
	}
}

function postnavbarHandler(htmltext)
{
	var doc = fromHTML(htmltext);
	var toggler = document.getElementById("navbar_creator_list");
	toggler.innerHTML = "";
	for (var i = 0; i < doc.length; i++) {
		if(doc[i].classList.contains("container"))
		{
			var tl = doc[i].getElementsByClassName("tree_list")[0].getElementsByTagName("a");
			console.log(tl, tl.length);
			for (var j = 0; j < tl.length; j++) {
				tl[j].classList.add("dropdown-item")
				//toggler.appendChild(wrapinli(tl[j]));
				//toggler.appendChild(tl[j]);
				toggler.appendChild(tl[j].cloneNode(true));
			}

			break;
		}

	}
}

function prenavbarHandler(url, postHandler)
{
	var toggler = document.getElementById("navbarDropdownMenuLink");
	if(toggler.getAttribute("aria-expanded") == 'false')
	{
		requestURL(url, postHandler);
	}
}

function selectCurrent()
{
	var currentlink = document.location.href;
	var x;
	if(currentlink.match('creations') != null)
	{
		x = document.getElementsByClassName('nav-item-creations')[0];
		x.className += ' active'; 
	}
	else if(currentlink.match('creators') != null)
	{
		x = document.getElementsByClassName('nav-item-creators')[0];
		x.className += ' active'; 
	}
	else if(currentlink.match('about') != null)
	{
		x = document.getElementsByClassName('nav-item-about')[0];
		x.className += ' active'; 
	}
	else
	{
		x = document.getElementsByClassName('nav-item-home')[0];
		x.className += ' active'; 
	}
	y = x.getElementsByClassName('sr-link');
	if (y.length > 0)
	{
		y[0].remove();
	}
	x.getElementsByClassName('nav-link')[0].innerHTML += '<span class="sr-only">(current)</span>';
	return x;
}

