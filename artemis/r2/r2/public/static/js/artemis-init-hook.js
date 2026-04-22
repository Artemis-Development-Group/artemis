/*
  Init modules defined in artemis-init.js

  requires r.hooks (hooks.js)
 */
!function(r) {
  r.hooks.get('artemis-init').register(function() {
    try {
        r.events.init();
        r.analytics.init();
        r.access.init();
    } catch (err) {
        r.sendError('Error during artemis-init.js init', err.toString());
    }
  })

  $(function() {
    r.hooks.get('artemis-init').call();
  });
}(r);
