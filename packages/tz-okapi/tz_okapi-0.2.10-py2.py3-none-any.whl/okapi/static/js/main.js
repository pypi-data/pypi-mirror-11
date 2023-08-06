$(function () {
  var toc = $('#toc');

  $('[data-toggle="tooltip"]').tooltip();

  $('.pre').click(function () {
    $(this).css('overflow', 'auto');
  });
  
  $('#contents > ul > li > ul').after('<li class="clear"></li>');

  var previous_level = 0;
  var previous_node = toc;

  $(':header').each(function (i) {
    if (i == 0) return;

    var current_node;
    var ul;
    var heading = $(this);
    var link = $('<a/>', {
      text: heading.text(),
      href: '#' + heading.parent().attr('id')
    });

    current_node = $('<li/>').append(link);
    var level = parseInt(heading.prop("tagName").substring(1));

    if (level > previous_level) {
      ul = $('<ul/>', {class: 'nav', role: 'tablist'});
      ul.append(current_node);
      previous_node.append(ul);
    } else if (level == previous_level) {
      previous_node.parent().append(current_node);
    } else if (level < previous_level) {
      ul = previous_node;
      for (var i=0; i < (previous_level - level)*2 + 1; i++) {
        ul = ul.parent();
      }
      ul.append(current_node);
    }

    previous_level = level;
    previous_node = current_node;

  });

});
