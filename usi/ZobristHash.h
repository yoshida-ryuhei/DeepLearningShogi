﻿#pragma once

#include "position.hpp"

struct node_hash_t {
	unsigned long long hash;
	int color;
	int moves;
	bool flag;
};

class UctHash
{
public:
	UctHash() : node_hash(nullptr) {}
	UctHash(const unsigned int hash_size) { InitializeUctHash(hash_size); }
	~UctHash() { delete[] node_hash; }

	//  UCTノードのハッシュの初期化
	void InitializeUctHash(const unsigned int hash_size);

	//  UCTノードのハッシュ情報のクリア
	void ClearUctHash(void);

	//  古いデータの削除
	void DeleteOldHash(const Position *pos);

	//  未使用のインデックスを探す
	unsigned int SearchEmptyIndex(const unsigned long long hash, const int color, const int moves);

	//  ハッシュ値に対応するインデックスを返す
	unsigned int FindSameHashIndex(const unsigned long long hash, const int color, const int moves) const;

	//  ハッシュ表が埋まっていないか確認
	bool CheckRemainingHashSize(void) const { return enough_size; }

	// ハッシュ使用率を取得(単位はパーミル(全体を1000とした値))
	int GetUctHashUsageRate() const { return 1000 * used / uct_hash_size; }

	// ノードを返す
	const node_hash_t& operator [](const size_t i) { return node_hash[i]; }

private:
	//  UCT用ハッシュテーブルのサイズ
	unsigned int uct_hash_size;
	unsigned int uct_hash_limit;

	//  UCT用ハッシュテーブル
	node_hash_t *node_hash;
	unsigned int used;
	bool enough_size;

	//  ハッシュテーブルのサイズの設定
	void SetHashSize(const unsigned int new_size);

	//  インデックスの取得
	unsigned int TransHash(const unsigned long long hash) const {
		return ((hash & 0xffffffff) ^ ((hash >> 32) & 0xffffffff)) & (uct_hash_size - 1);
	}

	// 古いハッシュの削除
	void delete_hash_recursively(Position &pos, const unsigned int index);
};
