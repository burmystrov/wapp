function uriSchemeWithHyperlinkFallback(uri, href) {
    // set up a timer and start it
    var start = new Date().getTime(),
        end,
        elapsed;

    // attempt to redirect to the uri:scheme
    // the lovely thing about javascript is that it's single threadded.
    // if this WORKS, it'll stutter for a split second, causing the timer to be off
    document.location = uri;

    // end timer
    end = new Date().getTime();

    elapsed = (end - start);

    // if there's no elapsed time, then the scheme didn't fire, and we head to the url.
    if (elapsed < 1) {
        document.location = href;
    } else {
        window.open(uri);
    }
}
