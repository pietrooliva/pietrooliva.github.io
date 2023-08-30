sceneEl.addEventListener("markerFound", (e) => {
    isMarkerVisible = true;
});

sceneEl.addEventListener("markerLost", (e) => {
    isMarkerVisible = false;
});
