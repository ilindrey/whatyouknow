$(document).ready(
    function () {

        let blocks_id_name = ["roof", "content", "floor"];

        for (let name_id of blocks_id_name)
        {
            let block_id = '#' + name_id;

            if ($(block_id).children().length === 0)
            {
                $(block_id).remove();
            }
        }

    }
);