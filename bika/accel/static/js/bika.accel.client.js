/**
 * Controller class for Client Add/Edit form
 */
function ClientEditForm() {

    var that = this;
    that.load = function() {
      handlePhysicalAddressValidator();
    }

    /**
    This function checks if PhysicalAddress field has State/Province and District
    options selected. It is important in Accel, because Client IDs will be
    generated by using abbreviations of PhysicalAddress.
    @param {String} id is id of the select list to validate
    */
    function handlePhysicalAddressValidator(){
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
    }

    /**
    This function checks if select list has selected item or no
    @param {String} id is id of the select list to validate
    */
    function isSelectEmpty(id){
      var slct = document.getElementById(id);
      var option = slct.options[slct.selectedIndex].value;
      if (option == null || option === "") {
        return true;
      }
      return false;
    }
  };
