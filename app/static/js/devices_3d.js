    // Random tree
    const N = 300;
    const gData = {
      nodes: [...Array(N).keys()].map(i => ({ id: i })),
      links: [...Array(N).keys()]
        .filter(id => id)
        .map(id => ({
          source: id,
          target: Math.round(Math.random() * (id-1))
        }))
    };

    const distance = 1400;

    const Graph = ForceGraph3D()
      (document.getElementById('3d-graph'))
        .width(1000)
        .height(500)
        .enableNodeDrag(false)
        .enableNavigationControls(false)
        .showNavInfo(false)
        .cameraPosition({ z: distance })
        .graphData(gData);

    // camera orbit
    let angle = 0;
    setInterval(() => {
      Graph.cameraPosition({
        x: distance * Math.sin(angle),
        z: distance * Math.cos(angle)
      });
      angle += Math.PI / 300;
    }, 10);


//// Random tree
//const N = 300;
//const gData = {
//  nodes: [...Array(N).keys()].map(i => ({ id: i })),
//  links: [...Array(N).keys()]
//    .filter(id => id)
//    .map(id => ({
//      source: id,
//      target: Math.round(Math.random() * (id-1))
//    }))
//};
//  
//const Graph = ForceGraph3D()
//(document.getElementById('3d-graph'))
//  .width(1000)
//  .height(500)
//  .graphData(gData);