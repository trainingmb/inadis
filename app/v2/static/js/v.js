// ==UserScript==
// @name         Get Most Recent
// @namespace    http://tampermonkey.net/
// @version      2024-05-30
// @description  try to take over the world!
// @author       You
// @match        https://kemono.su/patreon/user/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=kemono.su
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    async function sendContent()
    {
        var url = "http://stofgenius.pythonanywhere.com/api/v1/creators_reference/<creator_reference>/latest_posts"; 
        let response = await fetch(url.replace('<creator_reference>', window.location.href.split('/')[5]), {
            method: "GET",
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if(response.ok)
        {
            console.log("Got it");
            let jso = await response.json();
            console.log(jso);
            let l = '';
            for(let i = 0; i < jso.length; i++)
            {
                l += jso[i].name + " " + jso[i].latest_post.title;
            }
            alert(l);
        }
        else
        {
            console.log("Failed Retry");
        }
    }
    sendContent();
})();