/**
 * Controller class for Client Add/Edit form
 */
function ClientEditForm() {

    var that = this;
    that.load = function() {
      console.log('Client Edit');
      $('#client-base-edit').on('submit', function(e) {
        e.preventDefault();
        if(isSelectEmpty("PhysicalAddress.state")  || isSelectEmpty("PhysicalAddress.district")){
          alert('Please enter valid State/District for Physical Address');
          return false;
        }
        else{
          $('#client-base-edit')[0].submit();
        }
      });
      function isSelectEmpty(id){
        var slct = document.getElementById(id);
        var option = slct.options[slct.selectedIndex].value;
        if (option == null || option === "") {
          return true;
        }
        return false;
      }
    };
}
