
safeWrap();

function safeWrap()
{
    $(document).ready(
        function () {

            let blockNameList = ["roof", "content"];

            for (let blockName of blockNameList)
            {
                let block = $('#' + blockName);
                if (block.children().length === 0)
                {
                    block.closest('.row').remove();
                }
            }

            let authTitle = $('#auth_title');
            if(authTitle.length !== 0 && !authTitle.text())
            {
                authTitle.closest('.row').remove();
            }

        }
    );
}