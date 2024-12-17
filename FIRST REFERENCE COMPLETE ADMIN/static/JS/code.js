document.addEventListener("alpine:init", () => {
    Alpine.data("AutomatedDigitalMaturity", () => {
        return {
            Admin_Home_Page: true,
            manage_business_sector: false,
            manage_user_account: false,
            manage_csv_file_upload: false,
            activate_deactivate_user: false,
            computational_interface_new_business_sector: false,
            computational_interface_update_business_sector: false,
            assign_answer_rating_for_business_functions: false,

            select_business_sector: true,
            select_business_function: false,
            add_new_answer_rating:false,
            update_old_answer_rating:false,
            get_maturity_feedback:false,
            change_password:false,
            add_new_user:false,

            business_analysts_home_page:true,
            business_analysts_business_process_page:false,
            business_manager_home_page:false,
            

            // Added applications logics for business process and value chain 
            manage_business_process_data: false,
            manage_value_chain_data: false,
            add_new_value_chain_record:false,
            update_value_chain_record:false,

            add_new_business_process_record:false,
            update_business_process_record:false,
  
            openHomeBusinessAnalysts(BusinessAnalysts) {
                this.select_business_sector = true;
                this.select_business_function = false;
  
                if (BusinessAnalysts == "select_business_function") {
                    this.select_business_sector = false;
                    this.select_business_function = true;
                }
            },
  
            openHome(currentSection) {
                this.Admin_Home_Page = true;
                this.manage_business_sector = false;
                this.manage_user_account = false;
                this.manage_csv_file_upload = false;
                this.activate_deactivate_user = false;
                this.computational_interface_new_business_sector = false;
                this.computational_interface_update_business_sector = false;
                this.assign_answer_rating_for_business_functions = false;
                this.add_new_answer_rating=false;
                this.update_old_answer_rating=false;
                this.get_maturity_feedback=false;
                this.change_password = false;
                this.add_new_user=false;
                this.manage_business_process_data = false;
                this.manage_value_chain_data = false;
                this.add_new_value_chain_record =false;
                this.update_value_chain_record=false;
                this.add_new_business_process_record=false;
                this.update_business_process_record=false;
                this.business_analysts_home_page=true;
                this.business_analysts_business_process_page=false;
  
                if (currentSection == "manage_business_sector") {
                    this.Admin_Home_Page = false;
                    this.manage_business_sector = true;
                } else if (currentSection == "manage_user_account") {
                    this.Admin_Home_Page = false;
                    this.manage_user_account = true;
                } else if (currentSection == "add_new_answer_rating") {
                  this.Admin_Home_Page = false;
                  this.add_new_answer_rating = true;
              } else if (currentSection == "update_old_answer_rating") {
                  this.Admin_Home_Page = false;
                  this.update_old_answer_rating = true;
              } else if (currentSection == "manage_csv_file_upload") {
                    this.Admin_Home_Page = false;
                    this.manage_csv_file_upload = true;
                } else if (currentSection == "activate_deactivate_user") {
                    this.Admin_Home_Page = false;
                    this.activate_deactivate_user = true;
                } else if (currentSection == "computational_interface_new_business_sector") {
                    this.Admin_Home_Page = false;
                    this.computational_interface_new_business_sector = true;
                } else if (currentSection == "computational_interface_update_business_sector") {
                    this.Admin_Home_Page = false;
                    this.computational_interface_update_business_sector = true;
                } else if (currentSection == "assign_answer_rating_for_business_functions") {
                    this.Admin_Home_Page = false;
                    this.assign_answer_rating_for_business_functions = true;
                }else if (currentSection == "get_maturity_feedback") {
                  this.Admin_Home_Page = false;
                  this.get_maturity_feedback = true;
              }else if (currentSection == "change_password") {
                  this.Admin_Home_Page = false;
                  this.change_password = true;
              }else if (currentSection == "add_new_user") {
                  this.Admin_Home_Page = false;
                  this.add_new_user = true;
              }else if (currentSection == "manage_business_process_data") {
                this.Admin_Home_Page = false;
                this.manage_business_process_data = true;
            }else if (currentSection == "manage_value_chain_data") {
                this.Admin_Home_Page = false;
                this.manage_value_chain_data = true;
            }else if (currentSection == "update_business_process_record") {
                this.Admin_Home_Page = false;
                this.update_business_process_record = true;
            }else if (currentSection == "add_new_business_process_record") {
                this.Admin_Home_Page = false;
                this.add_new_business_process_record = true;
            }else if (currentSection == "update_value_chain_record") {
                this.Admin_Home_Page = false;
                this.update_value_chain_record = true;
            }else if (currentSection == "add_new_value_chain_record") {
                this.Admin_Home_Page = false;
                this.add_new_value_chain_record = true;
            }else if (currentSection == "business_analysts_business_process_page") {
                this.Admin_Home_Page = true;
                this.business_analysts_home_page=false;
                this.business_analysts_business_process_page = true;
            }
            },





              


          
  
            submitBusinessSector() {
                // Submit the form programmatically
                document.getElementById('business-sector-form').submit();
  
                // Change the state to show the business function section
                this.$nextTick(() => {
                    this.select_business_sector = false;
                    this.select_business_function = true;
                });
            },
  
            init() {
                this.startTimerWhyUs();
              //   this.activeImage = this.images.length > 0 ? this.images[0] : null;
            },
  
            images: [
                "/static/images/Looping/1.png",
                "/static/images/Looping/2.png",
                "/static/images/Looping/3.jpg",
                "/static/images/Looping/4.png",
            ],
            activeImage: null,
  
            prev() {
              this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
  
            },
  
            next() {
              this.currentIndex = (this.currentIndex + 1) % this.images.length;
            },
  
            imageWhyUs: [
                {
                    image: "/static/IMAGES/Looping/diamond curve.png",
                    text1: "THE DIAMOND RADAR PLOT",
                    text2: "Illustrates the transgression taking place in the digital maturity transformation phase within the different business functions from the As-Is to its To-Be state",
                },
                {
                    image: "./static/IMAGES/Looping/exponential.png",
                    text1: "THE EXPONENTIAL GROWTH CURVE",
                    text2: "Moving from the current state to the expected future state requires a significant focus on the business processes that is lagging the most. To help stakeholders with this informed data-driven decision making, the exponential growth curve was used to convey this knowledge. ",
                },
                
                {
                    image: "/static/IMAGES/Looping/bar plots.png",
                    text1: "THE BAR PLOTS",
                    text2: "The result obtained for the cumulative current, future and expected state from the business analyst submitted data are graphically relayed in a bar plot",
                },
               
                {
                    image: "/static/IMAGES/Looping/6.jpg",
                    text1: "THE BUSINESS PROCESSES",
                    text2: "Some few text description will come here for. Image will equally be changed 6",
                },
            ],
            currentIndex: 0,
  
            startTimerWhyUs() {
                setInterval(() => {
                  //   this.currentIndex = (this.currentIndex + 1) % this.imageWhyUs.length;
                  this.next();  
                  this.text1 = "";
                }, 6000);
            },
        };
    });
  });