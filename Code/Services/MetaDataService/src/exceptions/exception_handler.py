class ExceptionHandler:
    
    #add all the exceptions we are interested to handle here
    TIMEOUT_EXCEPTION = "ConnectTimeoutError"
    TIMEOUT_EXCEPTION_MSG = "There seems to be a network issue.\nPlease check your connectivity and try again."

    def handle_exception(self, ex):
        msg = ""
        if hasattr(ex, 'detail') and ex.detail is not None:
            msg = ex.detail
        else:
            msg = str(ex)

        errorMsg = msg
        if msg.find(self.TIMEOUT_EXCEPTION) != -1:
            errorMsg = self.TIMEOUT_EXCEPTION_MSG
        return errorMsg