    def merge(self):

        tiles = self.find_all_exist_tiles_position()
        tiles_will_merge = []

        for tile in reversed(range(len(tiles))):  # Tileler arasında büyükten küçüğe dolaş
            # sıradaki tile path
            current_tile = self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x]
            # eğer ilk satırda değilsek devam et
            if current_tile[tile].position.y != 0:
                tiles_will_merge.append(self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x])

            for tile in reversed(range(len(tiles))):  # Tileler arasında büyükten küçüğe dolaş
                # sıradaki tile path
                current_tile = self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x]

            # current tilenin altındaki tile pathı
            bottom_tile = self.tile_matrix[tiles_will_merge[tile].position.y - 1][tiles_will_merge[tile].position.x]
            # eğer none değilse konum ataması yap
            if bottom_tile is not None:
                # Alttaki cell boş orayı tail ile doldururuz
                bottom_tile.position = Point()
                bottom_tile.position.x = current_tile.position.x
                bottom_tile.position.y = current_tile.position.y
                bottom_tile.position.y -= 1

                # eğer numberları aynı ise merge işlemini gerçekleştir
                if current_tile.number == bottom_tile.number:
                    bottom_tile.tile_value_for_merge(current_tile.number + bottom_tile.number)
                    self.tile_matrix[tiles_will_merge[tile].position.y][tiles_will_merge[tile].position.x] = None
                    self.drop_tiles_2048()

        def drop_tiles_2048(self):

        tiles = self.find_all_exist_tiles_position()
        tiles_can_move_down = []

        for tile in range(len(tiles)):
            # tiles_can_move_down nın içi koşullara göre doldu
            if (self.tile_matrix[tiles[tile].position.y - 1][tiles[tile].position.x] is None) and (
                    tiles[tile].position.y != 0) and (
                    self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x - 1] is None) and (
                    self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x + 1] is None):
                tiles_can_move_down.append(self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x])

            # for tile_in_move_list in range(len(tiles_can_move_down)):
            #     stop = (self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y - 1][tiles_can_move_down[tile_in_move_list].position.x] is not None) or (tiles_can_move_down[tile_in_move_list].position.y != 0) or (self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x - 1] is not None) or (self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x + 1] is not None)
            #     while stop:
            #         drop_tile = self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x]
            #         self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y - 1][tiles_can_move_down[tile_in_move_list].position.x] = drop_tile
            #         self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x] = None
            #
            #         break

    def delete_tiles_2048(self):

        tiles = self.find_all_exist_tiles_position()
        tiles_can_move_down = []

        for tile in range(len(tiles)):
            # tiles_can_move_down nın içi koşullara göre doldu
            if (self.tile_matrix[tiles[tile].position.y - 1][tiles[tile].position.x] is None) and \
                    (tiles[tile].position.y != 0) and \
                    (self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x - 1] is None) and \
                    (self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x + 1] is None):
                tiles_can_move_down.append(self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x])

        for del_tiles in range(len(tiles_can_move_down)):
            self.tile_matrix[tiles_can_move_down[del_tiles].position.y][
                tiles_can_move_down[del_tiles].position.x] = None

        # for x in range(len(tiles_can_move_down)):
        #     print(tiles_can_move_down[x].position)
        # print("---------")
        # print("---------")
